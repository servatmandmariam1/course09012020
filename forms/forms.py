from flask_wtf import Form
from wtforms import StringField, IntegerField, SubmitField, HiddenField
from wtforms import validators


class PersonalDataForm(Form):
    age = IntegerField("Age: ", [
        validators.DataRequired("age"),
        validators.NumberRange(min=14, max=120)])
    weight = IntegerField("Weight: ", [
        validators.DataRequired("Weight"),
        validators.NumberRange(min=30, max=150)])
    height = IntegerField("Height: ", [
        validators.DataRequired("Height"),
        validators.NumberRange(min=100, max=200)])
    old_name = HiddenField()

    submit = SubmitField("Save")
class DishForm(Form):
    dishname = StringField("Dish name: ", [
        validators.DataRequired("Please enter dish name."),
        validators.Length(3, 100, "dish name should be from 3 to 100 symbols")])
    calories_amount = IntegerField("Calories amount: ", [
        validators.DataRequired("Please enter calories amount"), validators.NumberRange(min=1, max=5000)])
    receipt = StringField("Receipt: ", [
        validators.DataRequired("Please enter receipt."),
        validators.Length(3, 100, "receipt should be from 3 to 100 symbols")])
    ingridients =  StringField("Ingridients: ")
    type = StringField("Type:")
    old_name = HiddenField()

    submit = SubmitField("Save")
class ReceiptForm(Form):
    __tablename__ = 'receipt'
    dishname_fk = StringField("Dish name: ", [
        validators.DataRequired("Please enter dish name."),
        validators.Length(3, 255, "Name should be from 3 to 255 symbols")])
    receipt = StringField("Dish Receipt: ", [
        validators.DataRequired("Please enter dish Receipt."),
        validators.Length(3, 255, "Receipt should be from 3 to 255 symbols")])
    old_name = HiddenField()

    submit = SubmitField("Save")
class TypeForm(Form):
    typename = StringField("Type name: ", [
        validators.DataRequired("Please enter type name."),
        validators.Length(3, 255, "Name should be from 3 to 255 symbols")])
    dishname_fk = StringField("Dish name: ", [
        validators.DataRequired("Please enter dish name."),
        validators.Length(3, 255, "Name should be from 3 to 255 symbols")])
    old_name = HiddenField()
    old_type = HiddenField()

    submit = SubmitField("Save")
class RestorauntForm(Form):
    name = StringField("Name of restoraunt: ", [
        validators.DataRequired("Please enter name of restoraunt."),
        validators.Length(3, 255, "Name should be from 3 to 255 symbols")])
    dishname_fk = StringField("Dish name: ", [
        validators.DataRequired("Please enter dish name."),
        validators.Length(3, 255, "Name should be from 3 to 255 symbols")])
    star = IntegerField("Star of restoraunt: ", [
        validators.DataRequired("Please enter star of restoraunt."),
        validators.NumberRange(min=1, max=5)]
                        )

    country = StringField("country of restoraunt: ", [
        validators.DataRequired("Please enter country of restoraunt."),
        validators.Length(3, 255, "country should be from 3 to 255 symbols")])
    city = StringField("city of restoraunt: ", [
        validators.DataRequired("Please enter city of restoraunt."),
        validators.Length(3, 20, "city should be from 3 to 255 symbols")])
    address = StringField("adress of restoraunt: ", [
        validators.DataRequired("Please enter adress of restoraunt."),
        validators.Length(3, 20, "adress should be from 3 to 255 symbols")])
    old_name = HiddenField()
    submit = SubmitField("Save")


class IngridientForm(Form):
    ingridients = StringField("Ingridients: ", [
        validators.DataRequired("Please enter dish ingridients."),
        validators.Length(3, 255, "Ingridient should be from 3 to 255 symbols")])
    old_name = HiddenField()

#     submit = SubmitField("Save")