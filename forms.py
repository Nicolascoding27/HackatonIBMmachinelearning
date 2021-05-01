from flask_wtf import FlaskForm
from flask_wtf import Form
from wtforms import StringField, TextField, SubmitField, IntegerField,TextAreaField,RadioField,SelectField, DecimalField
from wtforms.validators import DataRequired
from wtforms.validators import Length
from wtforms.validators import ValidationError

class PredictForm(FlaskForm):
    Unnamed=IntegerField('Unnamed:0')
    Cliente=IntegerField('Cliente')    
    Pais = StringField('Pais(Peru,Colombia,Ecuador')
    Moneda = StringField('Moneda')
    Unidad = StringField('Unidad')
    MesVencimiento = IntegerField('MesVencimiento')
    Monto = IntegerField('Monto')
    plazo = IntegerField('plazo')
    Prob_D = DecimalField('Prob_D')
    submit = SubmitField('Predict')
    abc = "" # this variable is used to send information back to the front page
    ammount=""
