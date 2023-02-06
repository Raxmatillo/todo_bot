from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

week_cd = CallbackData("show", "week")



weeks = {
    "Dushanba": "monday",
    "Seshanba": "tuesday",
    "Chorshanba": "wednesday",
    "Payshanba": "thursday",
    "Juma": "friday",
    "Shanba": "saturday",
    # "Yakshanba": "Sunday"
}

markup = InlineKeyboardMarkup(row_width=3)

for day_uz, day_eng in weeks.items():
    markup.insert(
        InlineKeyboardButton(
            text=day_uz,
            callback_data=week_cd.new(week=day_eng)
        )
    )

markup.row(
    InlineKeyboardButton(
        text="Bekor qilish",
        callback_data=week_cd.new(week="cancel")
    )
)

