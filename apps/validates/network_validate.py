from wtforms import StringField, Form, IntegerField
from wtforms.validators import DataRequired, Regexp, AnyOf, Optional, IPAddress
from . import Config


class AddNetworkAccountForm(Form):
    place = StringField(validators=[
        DataRequired(message='The place cannot be empty'),
        AnyOf(values=Config.places(), message='The entered place is not within the specified range')
    ])
    name = StringField(validators=[DataRequired(message='The customer name cannot be empty')])
    vlan = IntegerField(validators=[Optional()])
    start_ip = StringField(validators=[
        DataRequired(message='The start ip address cannot be empty'),
        IPAddress(message='The start ip address does not conform to the specification')
    ])
    end_ip = StringField(validators=[
        DataRequired(message='The end ip address cannot be empty'),
        IPAddress(message='The end ip address does not conform to the specification')
    ])
    mask_router_dns = StringField(validators=[
        DataRequired(message='The mask and router and dns cannot be empty'),
        Regexp(regex=Config.route_regex(), message='The format of mask, router or dns must be wrong')
    ])
    topology = StringField(
        DataRequired(message='The topology cannot be empty'),
        Regexp(regex=r'')
    )
