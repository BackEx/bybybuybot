"use strict";
define(['backbonekts', 'models/salesman'], function (BackboneKTS, SalesMan) {
    return BackboneKTS.Collection.extend({
        model: SalesMan,
        url: function () {
            return config.getMethodUrl('salesman.get', {
                offset: this.offset,
                count: this.pageSize
            });
        }
    });
});