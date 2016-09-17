"use strict";
define([
    'backbonekts', 'underscore', 'jquery',
    'text!templates/salesmen/index.html',
    'text!templates/salesmen/form.html',
    'collections/salesmen', 'models/salesman'
], function (BackboneKTS, _, $, indexTemplate, formTemplate, SalesmenCollection, Salesman) {
    return BackboneKTS.View.extend({
        indexTemplate: _.template(indexTemplate),
        formTemplate: _.template(formTemplate),
        events: {
            'click .pagination__item.pagination__item_salesmen': 'pagination',
            'submit .js-corp-form': 'formSubmit',
            'click .js-salesman-remove': 'removeSalesman'
        },
        actionIndex: function (offset) {
            var self = this;
            if (offset === null) {
                offset = 0;
            }
            var salesmenCollection = new SalesmenCollection();
            salesmenCollection.fetch({
                data: {
                    offset: offset
                },
                success: function () {
                    self.$el.html(self.indexTemplate({
                        offset: offset,
                        count: salesmenCollection.totalCount,
                        users: salesmenCollection
                    }));
                }
            });
        },
        actionEdit: function (id) {
            this._actionPut(id);
        },
        _actionPut: function (id) {
            var self = this;

            function render(item) {
                self.$el.html(self.formTemplate({
                    item: item
                }));
            }

            if (id !== undefined) {
                var salesman = new Salesman({id: id});
                salesman.fetch({
                    success: function () {
                        render(salesman);
                    }
                });
            } else {
                render(new Salesman());
            }
        },
        formSubmit: function (evt) {
            var self = this,
                data = self.serializeForm(evt.currentTarget);
            evt.preventDefault();

            var salesman = new Salesman();
            salesman.save(data, {
                url: config.getMethodUrl('salesman.save'),
                success: function () {
                    if (data.id) {
                        self._showSuccess('Успех', 'Администратор успешно сохранен');
                    }
                    self.redirect('salesmen');
                },
                error: function (object, response) {
                    self._showError(response);
                }
            });
        },
        removeSalesman: function (e) {
            e.preventDefault();
            var id = $(e.currentTarget).attr('data-id');
            var self = this;
            if (confirm('Вы уверены?')) {
                $.ajax({
                    method: 'post',
                    url: config.getMethodUrl('salesman.delete', {id: id}),
                    success: function () {
                        self._showSuccess('Успех', 'Продавец удален');
                        $('.js-salesman-row[data-id="' + id + '"]').remove();
                    }
                });
            }
        },
        pagination: function (e) {
            var self = this,
                offset = $(e.currentTarget).attr('data-offset');
            e.preventDefault();
            self.actionIndex(offset);
        }
    });
});