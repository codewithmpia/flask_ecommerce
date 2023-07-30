from flask_wtf import FlaskForm
from wtforms.fields import IntegerField, StringField, PasswordField, EmailField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Email, EqualTo


class QuantityForm(FlaskForm):
    quantity = IntegerField(
        label="Quantité",
        validators=[NumberRange(min=1, max=20), DataRequired()],
        default="1"
    )
    submit = SubmitField(label="Ajouter")


class RegisterForm(FlaskForm):
    username = StringField(
        label="Nom d'utlisateur",
        validators=[DataRequired()]
    )
    email = EmailField(
        label="Votre adresse mail",
        validators=[
            DataRequired(),
            Email()
        ]
    )
    password = PasswordField(
        label="Mot de passe",
        validators=[
            DataRequired(),
            EqualTo("confirm", message="Les mots de passe ne correspondent pas.")
        ]
    )
    confirm = PasswordField(
        label="Confirmer le mot de passe",
        validators=[DataRequired()]
    )
    submit = SubmitField(label="S'inscrire")


class LoginForm(FlaskForm):
    username = StringField(
        label="Nom d'utilisateur",
        validators=[DataRequired()]
    )
    password = PasswordField(
        label="Mot de passe",
        validators=[DataRequired()]
    )
    submit = SubmitField(label="Se connecter")