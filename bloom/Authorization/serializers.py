from rest_framework import serializers
from user.models import CustomUser
from django.contrib.auth import get_user_model

MIN_LENGTH = 8


class RegistrationSerializer(serializers.ModelSerializer):
  password = serializers.CharField(
    write_only=True,
    min_length=MIN_LENGTH,
    error_messages={
      "min_length": f"Password must be longer than {MIN_LENGTH} characters."
    },
    style={'input_type': 'password', 'placeholder': 'Password'}
  )
  password2 = serializers.CharField(
    write_only=True,
    min_length=MIN_LENGTH,
    error_messages={
      "min_length": f"Password must be longer than {MIN_LENGTH} characters."
    },
    style={'input_type': 'password', 'placeholder': 'Password'}
  )
  
  class Meta:
    model = CustomUser
    fields = ('username', 'email', 'password', 'password2', 'first_name', 'last_name', 'street', 'city', 'zip_code', 'country')
    extra_kwargs = {
      "username": {"write_only": True, "required": True},
      "first_name": {"write_only": True, "required": True},
      "last_name": {"write_only": True, "required": True},
      "email": {"write_only": True, "required": True},
      "password": {"write_only": True , "required": True},
      "password2": {"write_only": True , "required": True},
      "street": {"write_only": True , "required": True},
      "city": {"write_only": True , "required": True},
      "zip_code": {"write_only": True , "required": True},
      "country": {"write_only": True , "required": True},

    }

  def validate(self, data):
    if data["password"] != data["password2"]:
      raise serializers.ValidationError("Password does not match.")
    
    email = data["email"]
    if CustomUser.objects.filter(email=email).exists():
      raise serializers.ValidationError("Email is already in use.")
    return data
   
  
  def create(self, validated_data,):
    user = CustomUser.objects.create(
      username=validated_data["username"],
      first_name=validated_data["first_name"],
      last_name=validated_data["last_name"],
      email=validated_data["email"],
      street=validated_data["street"],
      city=validated_data["city"],
      zip_code=validated_data["zip_code"],
      country=validated_data["country"]

    )
    user.is_active = False
    user.set_password(validated_data["password"])
    user.save()

    return user

def authenticate_with_username_and_password(username, password):
    user = get_user_model()
    try:
        user = user.objects.get(username=username)
        if user.check_password(password):
            return user
    except user.DoesNotExist:
        return None

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True,write_only=True)
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password', 'placeholder': 'Password'})
    
    class Meta:
        model = CustomUser
        fields = ('username','password')
        read_only_fields = ('username', )

    def validate(self, data):
        user = authenticate_with_username_and_password(data["username"], data["password"])
        if user:
            if user.is_active:
                return {'username': user.username, 'email': user.email, 'password': user.password}
        raise serializers.ValidationError("Incorrect Credentials")