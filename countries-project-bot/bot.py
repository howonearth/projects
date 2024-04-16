from countries_list import format_text

from telegram.ext import ContextTypes, Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ConversationHandler
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from typing import Final
import random
from cs50 import SQL


class Country:
    def __init__(self, name="None"):
        self.country = name
        self.foods = []

    @property
    def country(self):
        return self._country

    @country.setter
    def country(self, name):
        # List of countries of the world
        countries = ["None", 'Afghanistan', 'Albania', 'Algeria', 'Andorra', 'Angola', 'Antigua and Barbuda', 'Argentina', 'Armenia', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin', 'Bhutan', 'Bolivia', 'Bosnia and Herzegovina', 'Botswana', 'Brazil', 'Brunei', 'Bulgaria', 'Burkina Faso', 'Burundi', "Côte d'Ivoire", 'Cabo Verde', 'Cambodia', 'Cameroon', 'Canada', 'Central African Republic', 'Chad', 'Chile', 'China', 'Colombia', 'Comoros', 'Congo (Congo-Brazzaville)', 'Costa Rica', 'Croatia', 'Cuba', 'Cyprus', 'Czechia (Czech Republic)', 'Democratic Republic of the Congo', 'Denmark', 'Djibouti', 'Dominica', 'Dominican Republic', 'Ecuador', 'Egypt', 'El Salvador', 'Equatorial Guinea', 'Eritrea', 'Estonia', '"Eswatini (fmr. ""Swaziland"")"', 'Ethiopia', 'Fiji', 'Finland', 'France', 'Gabon', 'Gambia', 'Georgia', 'Germany', 'Ghana', 'Greece', 'Grenada', 'Guatemala', 'Guinea', 'Guinea-Bissau', 'Guyana', 'Haiti', 'Holy See', 'Honduras', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran', 'Iraq', 'Ireland', 'Israel', 'Italy', 'Jamaica', 'Japan', 'Jordan', 'Kazakhstan', 'Kenya', 'Kiribati', 'Kuwait', 'Kyrgyzstan', 'Laos', 'Latvia', 'Lebanon', 'Lesotho', 'Liberia', 'Libya', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Madagascar', 'Malawi', 'Malaysia', 'Maldives', 'Mali', 'Malta', 'Marshall Islands', 'Mauritania', 'Mauritius', 'Mexico', 'Micronesia', 'Moldova', 'Monaco', 'Mongolia', 'Montenegro', 'Morocco', 'Mozambique', 'Myanmar (formerly Burma)', 'Namibia', 'Nauru', 'Nepal', 'Netherlands', 'New Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'North Korea', 'North Macedonia', 'Norway', 'Oman', 'Pakistan', 'Palau', 'Palestine State', 'Panama', 'Papua New Guinea', 'Paraguay', 'Peru', 'Philippines', 'Poland', 'Portugal', 'Qatar', 'Romania', 'Russia', 'Rwanda', 'Saint Kitts and Nevis', 'Saint Lucia', 'Saint Vincent and the Grenadines', 'Samoa', 'San Marino', 'Sao Tome and Principe', 'Saudi Arabia', 'Senegal', 'Serbia', 'Seychelles', 'Sierra Leone', 'Singapore', 'Slovakia', 'Slovenia', 'Solomon Islands', 'Somalia', 'South Africa', 'South Korea', 'South Sudan', 'Spain', 'Sri Lanka', 'Sudan', 'Suriname', 'Sweden', 'Switzerland', 'Syria', 'Tajikistan', 'Tanzania', 'Thailand', 'Timor-Leste', 'Togo', 'Tonga', 'Trinidad and Tobago', 'Tunisia', 'Turkey', 'Turkmenistan', 'Tuvalu', 'Uganda', 'Ukraine', 'United Arab Emirates', 'United Kingdom', 'United States of America', 'Uruguay', 'Uzbekistan', 'Vanuatu', 'Venezuela', 'Vietnam', 'Yemen', 'Zambia', 'Zimbabwe']
        name = format_text(name)
        if name not in countries:
            raise ValueError("Invalid country name")
        self._country = name

    def add_dish(self, name, rating):
        self.foods.append({"dish": name, "rating": rating})



TOKEN: Final = # TOKEN 
BOT_USERNAME: Final = "@countries_project_bot"


#constants for the conversation handler
DISH, RATING, COUNTRY = range(3)


#countries = ['Afghanistan', 'Albania', 'Algeria', 'Andorra', 'Angola', 'Antigua and Barbuda', 'Argentina', 'Armenia', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin', 'Bhutan', 'Bolivia', 'Bosnia and Herzegovina', 'Botswana', 'Brazil', 'Brunei', 'Bulgaria', 'Burkina Faso', 'Burundi', "Côte d'Ivoire", 'Cabo Verde', 'Cambodia', 'Cameroon', 'Canada', 'Central African Republic', 'Chad', 'Chile', 'China', 'Colombia', 'Comoros', 'Congo (Congo-Brazzaville)', 'Costa Rica', 'Croatia', 'Cuba', 'Cyprus', 'Czechia (Czech Republic)', 'Democratic Republic of the Congo', 'Denmark', 'Djibouti', 'Dominica', 'Dominican Republic', 'Ecuador', 'Egypt', 'El Salvador', 'Equatorial Guinea', 'Eritrea', 'Estonia', '"Eswatini (fmr. ""Swaziland"")"', 'Ethiopia', 'Fiji', 'Finland', 'France', 'Gabon', 'Gambia', 'Georgia', 'Germany', 'Ghana', 'Greece', 'Grenada', 'Guatemala', 'Guinea', 'Guinea-Bissau', 'Guyana', 'Haiti', 'Holy See', 'Honduras', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran', 'Iraq', 'Ireland', 'Israel', 'Italy', 'Jamaica', 'Japan', 'Jordan', 'Kazakhstan', 'Kenya', 'Kiribati', 'Kuwait', 'Kyrgyzstan', 'Laos', 'Latvia', 'Lebanon', 'Lesotho', 'Liberia', 'Libya', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Madagascar', 'Malawi', 'Malaysia', 'Maldives', 'Mali', 'Malta', 'Marshall Islands', 'Mauritania', 'Mauritius', 'Mexico', 'Micronesia', 'Moldova', 'Monaco', 'Mongolia', 'Montenegro', 'Morocco', 'Mozambique', 'Myanmar (formerly Burma)', 'Namibia', 'Nauru', 'Nepal', 'Netherlands', 'New Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'North Korea', 'North Macedonia', 'Norway', 'Oman', 'Pakistan', 'Palau', 'Palestine State', 'Panama', 'Papua New Guinea', 'Paraguay', 'Peru', 'Philippines', 'Poland', 'Portugal', 'Qatar', 'Romania', 'Russia', 'Rwanda', 'Saint Kitts and Nevis', 'Saint Lucia', 'Saint Vincent and the Grenadines', 'Samoa', 'San Marino', 'Sao Tome and Principe', 'Saudi Arabia', 'Senegal', 'Serbia', 'Seychelles', 'Sierra Leone', 'Singapore', 'Slovakia', 'Slovenia', 'Solomon Islands', 'Somalia', 'South Africa', 'South Korea', 'South Sudan', 'Spain', 'Sri Lanka', 'Sudan', 'Suriname', 'Sweden', 'Switzerland', 'Syria', 'Tajikistan', 'Tanzania', 'Thailand', 'Timor-Leste', 'Togo', 'Tonga', 'Trinidad and Tobago', 'Tunisia', 'Turkey', 'Turkmenistan', 'Tuvalu', 'Uganda', 'Ukraine', 'United Arab Emirates', 'United Kingdom', 'United States of America', 'Uruguay', 'Uzbekistan', 'Vanuatu', 'Venezuela', 'Vietnam', 'Yemen', 'Zambia', 'Zimbabwe']
db = SQL("sqlite:///countries.db")
country = Country("None")

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text("Welcome to the Project: Countries of the World!")
    await update.message.reply_text("If you want to add a country, tell me its name. \n\n If you want to get a random country, press /random")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Here is how this bot works: \n /start to start \n /help to get help \n /random to get a random country \n /best to get the list of dishes you rated 7/10 and higher")


async def random_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    c_list = db.execute("SELECT * FROM countries WHERE done = ?", "no")
    countries = []
    for country in c_list:
        countries.append(country["country"])
    country = random.choice(countries)
    await update.effective_message.reply_text(f"{country}")


async def best_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    dishes = db.execute("SELECT * FROM foods")
    TEXT = []
    TEXT.append("List of dishes you liked the most: \n")
    best = filter(lambda r: r["rating"] > 6, dishes)
    for dish in best:
        country_name = db.execute("SELECT country FROM countries WHERE id = ?", dish["country_id"])[0]["country"]
        print(country_name)
        TEXT.append(f"- {dish['food']} ({country_name})")

    await update.effective_message.reply_text("\n".join(TEXT))


def add_country(text: str) -> int:
    id_d = db.execute("SELECT id FROM countries WHERE country = ?", text)
    country_id = id_d[0]["id"]
    db.execute("UPDATE countries SET done = ? WHERE id = ?", "yes", country_id)
    return country_id


async def add_country_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    country_name = text.strip()
    global country
    country.country = country_name
    await update.effective_message.reply_text(f"{country.country} added! \nWhat dish from {country.country} did you cook? \n\nIf you don't want to add any dishes, press /done")
    return DISH


async def add_dish(update: Update, context:ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    dish = text.strip().title()
    RATING_MARKUP = InlineKeyboardMarkup([
            [InlineKeyboardButton('1', callback_data=f'1/{dish}'),
            InlineKeyboardButton('2', callback_data=f'2/{dish}'),
            InlineKeyboardButton('3', callback_data=f'3/{dish}')],
            [InlineKeyboardButton('4', callback_data=f'4/{dish}'),
            InlineKeyboardButton('5', callback_data=f'5/{dish}'),
            InlineKeyboardButton('6', callback_data=f'6/{dish}')],
            [InlineKeyboardButton('7', callback_data=f'7/{dish}'),
            InlineKeyboardButton('8', callback_data=f'8/{dish}'),
            InlineKeyboardButton('9', callback_data=f'9/{dish}')],
            [InlineKeyboardButton('10', callback_data=f'10/{dish}')]
                ])
    await update.effective_message.reply_text('Rate the dish from 1 to 10 where \n 1 = "We hated it!" and \n 10 = "We loved it!"', reply_markup=RATING_MARKUP)
    return RATING


async def rating(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    data = update.callback_query.data
    rating, plate = data.split("/")
    country.add_dish(plate, rating)
    await update.effective_message.reply_text(f"{plate}: rated!")
    await update.effective_message.reply_text("If you want to add another dish, write and send its name. \n\n If you don't, press /done")
    return DISH


async def done(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global country
    country_id = add_country(country.country)
    TEXT = []
    TEXT.append(f"Country: {country.country}")
    foods = country.foods
    print(foods)
    for food in foods:
        db.execute("INSERT INTO foods(country_id, food, rating) VALUES (?, ?, ?)", country_id, food['dish'], food['rating'])
        TEXT.append(f"Dish: {food['dish']} - {food['rating']}/10")
    await update.effective_message.reply_text("\n".join(TEXT))
    await update.effective_message.reply_text("All saved!")
    country.country = "None"
    country.foods = []
    return ConversationHandler.END


if __name__ == '__main__':
    print("Starting bot...")
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("random", random_command))
    app.add_handler(CommandHandler("best", best_command))


    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.TEXT, add_country_handler)],
        states={
            DISH:[
                CommandHandler("done", done),
                MessageHandler(filters.TEXT, add_dish)
                ],
            RATING: [CallbackQueryHandler(rating)]
        },
        fallbacks=[CommandHandler("done", done)],
    )

    app.add_handler(conv_handler)

    print("Polling...")
    app.run_polling()
