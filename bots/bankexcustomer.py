# coding=utf-8
import traceback

from tornkts import utils
from models.bankex import User, Offer
from models.content import Text
from roboman.bot import BaseBot
from roboman.keyboard import ReplyKeyboard, ReplyKeyboardHide, InlineKeyboard, InlineKeyboardButton
from settings import options
import logging
import datetime
import re

logger = logging.getLogger('bank_ex_customer')


class BankExCustomer(BaseBot):
    name = 'TestBankExCustomer'
    key = options.key_bank_ex_customer

    @classmethod
    def num_split(cls, num):
        s = '%d' % num
        groups = []
        while s and s[-1].isdigit():
            groups.append(s[-3:])
            s = s[:-3]
        return s + ' '.join(reversed(groups))

    @classmethod
    def before_hook(cls, data):
        try:
            user = User.objects.get(out_id=data.get('from_id'))
            user.username = data.get('from_username')
            user.save()
        except User.DoesNotExist:
            user = User(
                out_id=data.get('from_id'),
                name=data.get('from_first_name'),
                surname=data.get('from_last_name'),
                username=data.get('from_username')
            )
            user.save()

        data['user'] = user
        return data

    @classmethod
    def on_hook(cls, data):
        user = data['user']
        text = data.get('text')

        if cls.match_command('/start', text) or cls.match_command(Text.format('CL_MSG_NEW_SEARCH'), text):
            return cls._on_start(**data)
        if not user.location:
            return cls._on_enter_location(**data)
        elif len(user.tags) == 0:
            return cls._on_enter_tags(**data)
        elif not user.price:
            return cls._on_enter_price(**data)

        if data.get('callback_query'):
            user.step = User.STEP_BLOCKCHAIN
            user.save()

            keyboard = ReplyKeyboard(keyboard=[[
                Text.format('CL_YES_APPROVE'),
                Text.format('CL_NO_FEAR'),
                Text.format('CL_WHAT_IS_BLOCKCHAIN'),
            ]])

            cls.send(
                chat_id=data.get('chat_id'),
                text=Text.format('CL_MSG_CHOOSE_OFFER'),
                reply_markup=keyboard.to_json()
            )
            cls.answer_callback_query(callback_query_id=data.get('callback_query_id'))
            return

        if user.step == User.STEP_BLOCKCHAIN:
            return cls._on_choose_blockchain(**data)
        elif user.step == User.STEP_QIWI:
            return cls._on_choose_qiwi(**data)

        if cls.match_command(Text.format('CL_MSG_ALL_UNDERSTAND'), text) \
                or cls.match_command(Text.format('CL_MSG_NEXT'), text):
            cls._next_item(**data)
        elif cls.match_command(Text.format('CL_MSG_PREVIOUS'), text):
            cls._prev_item(**data)
        elif cls.match_command(Text.format('CL_MSG_NEW_SEARCH'), text):
            cls._on_start(**data)
        elif cls.match_command('/hackend', text):
            cls._on_hachend(**data)

    @classmethod
    def _on_start(cls, **kwargs):
        user = kwargs['user']

        user.location = None
        user.tags = []
        user.price = None
        user.offset = 0
        user.step = User.STEP_CHOOSING
        user.save()

        cls.send(
            chat_id=kwargs.get('chat_id'),
            text=Text.format('CL_MSG_WELCOME'),
            reply_markup=ReplyKeyboardHide().to_json()
        )

    @classmethod
    def _on_hachend(cls, **kwargs):
        now = datetime.datetime.now()
        end = datetime.datetime(2016, 9, 18, 12, 0)
        diff = (end - now)
        cls.send(
            chat_id=kwargs.get('chat_id'),
            text=u"До конца хакатона %s:%s" % (diff.seconds / 3600, diff.seconds % 3600 / 60),
        )

    @classmethod
    def _on_enter_location(cls, **kwargs):
        user = kwargs['user']
        user.location = kwargs.get('text')
        user.save()

        cls.send(chat_id=kwargs.get('chat_id'), text=Text.format('CL_MSG_ENTER_TAGS'))

    @classmethod
    def _on_enter_tags(cls, **kwargs):
        user = kwargs['user']
        tags = kwargs.get('text', '').split(',')
        for i, tag in enumerate(tags):
            tags[i] = re.sub(r'$', '', tag)

        user.tags = tags
        user.save()

        cls.send(chat_id=kwargs.get('chat_id'), text=Text.format('CL_MSG_ENTER_PRICE'))

    @classmethod
    def _on_enter_price(cls, **kwargs):
        user = kwargs['user']
        user.price = utils.to_int(kwargs.get('text'))
        user.save()

        if not user.price:
            return cls.send(
                chat_id=kwargs.get('chat_id'),
                text=Text.format('CL_MSG_SEND_NUMBER'),
            )

        keyboard = ReplyKeyboard(keyboard=[
            [Text.format('CL_MSG_ALL_UNDERSTAND')]
        ])

        cls.send(
            chat_id=kwargs.get('chat_id'),
            text=Text.format('CL_MSG_COMPLETE_FILL_INFO'),
            reply_markup=keyboard.to_json()
        )

    @classmethod
    def _on_choose_blockchain(cls, **data):
        user = data.get('user')
        text = data.get('text')

        if cls.match_command(Text.format('CL_YES_APPROVE'), text):
            user.step = User.STEP_QIWI
            user.save()
            cls.send(
                chat_id=data.get('chat_id'),
                text=Text.format('CL_REG_QIWI'),
                reply_markup=ReplyKeyboard(keyboard=[[
                    Text.format('CL_YES_APPROVE'),
                    Text.format('CL_WANT_SPENT_MONEY'),
                    Text.format('CL_WHAT_IS_QIWI'),
                ]])
            )
        elif cls.match_command(Text.format('CL_NO_FEAR'), text):
            user.step = User.STEP_CHOOSING
            user.save()
            cls.send(
                chat_id=data.get('chat_id'),
                text=Text.format('CL_FEAR_BLOCKCHAIN_WIKI'),
                reply_markup=cls._get_main_keyboard().to_json()
            )
        elif cls.match_command(Text.format('CL_WHAT_IS_BLOCKCHAIN'), text):
            user.step = User.STEP_CHOOSING
            user.save()
            cls.send(
                chat_id=data.get('chat_id'),
                text=Text.format('CL_WHAT_IS_BLOCKCHAIN_WIKI'),
                reply_markup=cls._get_main_keyboard().to_json()
            )

    @classmethod
    def _on_choose_qiwi(cls, **data):
        user = data.get('user')
        text = data.get('text')

        if cls.match_command(Text.format('CL_YES_APPROVE'), text):
            user.step = User.STEP_CHOOSING
            user.save()
            cls.send(
                chat_id=data.get('chat_id'),
                text=Text.format('CL_BEGIN_DEAL'),
                reply_markup=cls._get_main_keyboard().to_json()
            )
        elif cls.match_command(Text.format('CL_WANT_SPENT_MONEY'), text):
            user.step = User.STEP_CHOOSING
            user.save()
            cls.send(
                chat_id=data.get('chat_id'),
                text=Text.format('CL_CANNOT_SPEND_MONEY'),
                reply_markup=cls._get_main_keyboard().to_json()
            )
        elif cls.match_command(Text.format('CL_WHAT_IS_QIWI'), text):
            user.step = User.STEP_CHOOSING
            user.save()
            cls.send(
                chat_id=data.get('chat_id'),
                text=Text.format('CL_QIWI_DESCRIPTION'),
                reply_markup=cls._get_main_keyboard().to_json()
            )

    @classmethod
    def _show_item(cls, **kwargs):
        user = kwargs['user']

        keyboard = cls._get_main_keyboard()

        offers = Offer.objects.skip(user.offset).limit(1)
        if len(offers) == 0:
            cls.send(
                chat_id=kwargs.get('chat_id'),
                text=Text.format('CL_MSG_NO_MORE'),
                reply_markup=keyboard.to_json()
            )
            return

        for offer in offers:
            try:
                with open(offer.rendered_img_abs, 'rb') as f:
                    inline_keyboard = InlineKeyboard(keyboard=[
                        [InlineKeyboardButton(text=u'Купить', callback_data=offer.get_id())]
                    ])
                    cls.send_photo(
                        files={'photo': ('img.png', f.read(), 'image/png', {})},
                        chat_id=kwargs.get('chat_id'),
                        reply_markup=inline_keyboard.to_json()
                    )
                    if user.offset == 0:
                        cls.send(
                            chat_id=kwargs.get('chat_id'),
                            text=Text.format('CL_MSG_NAV_HINT'),
                            reply_markup=keyboard.to_json()
                        )
            except Exception as e:
                traceback.print_exc()
                cls.send(
                    chat_id=kwargs.get('chat_id'),
                    text=Text.format('CL_MSG_IMAGE_NOT_FOUND'),
                    reply_markup=keyboard.to_json()
                )

    @classmethod
    def _prev_item(cls, **kwargs):
        user = kwargs['user']

        cls._show_item(**kwargs)

        user.offset -= 1
        if user.offset < 0:
            user.offset = 0
        user.save()

    @classmethod
    def _next_item(cls, **kwargs):
        user = kwargs['user']

        cls._show_item(**kwargs)

        user.offset += 1
        user.save()

    @classmethod
    def _get_main_keyboard(cls):
        return ReplyKeyboard(keyboard=[[
            Text.format('CL_MSG_PREVIOUS'),
            Text.format('CL_MSG_NEW_SEARCH'),
            Text.format('CL_MSG_NEXT'),
        ]], one_time_keyboard=False)
