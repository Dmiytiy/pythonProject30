from django.forms.models import model_to_dict
#1) В этом примере мы получаем текущего пользователя из контекста запроса (self.context['request'].user) и
# присваиваем его в validated_data перед созданием объекта Entity с помощью метода create() модели Entity.
class EntitySerializer(ModelSerializer):
    value = IntegerField(...)
    properties = PropertySerializer(many=True, read_only=True)

    def create(self, validated_data):
        user = self.context['request'].user
        entity = Entity.objects.create(modified_by=user, **validated_data)
        return entity
#2)В этом примере мы указываем, что значение для поля value нужно брать из поля 'data[value]'
# входного JSON (с помощью параметра source='data[value]').

#Далее мы в методе create() явно указываем, что нужно сохранять значение из поля 'data[value]'
# в поле value модели Entity при создании объекта.
class EntitySerializer(ModelSerializer):
    value = IntegerField(source='data[value]')
    properties = PropertySerializer(many=True, read_only=True)

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['modified_by'] = user
        entity = Entity.objects.create(value=validated_data['data']['value'], modified_by=user)
        return entity


#В этом примере мы добавили поле properties с помощью SerializerMethodField(), чтобы определить свой метод get_properties() для его заполнения.

#В методе get_properties() мы создаем пустой словарь properties и обходим все свойства объекта Entity,
# преобразуя их в словарь с помощью метода model_to_dict(). Затем мы добавляем эти словари в общий словарь
# properties,
#где ключами будут значения поля key из модели Property, а значениями - значения поля value.
class EntitySerializer(ModelSerializer):
    value = IntegerField(source='data[value]')
    properties = SerializerMethodField()

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['modified_by'] = user
        entity = Entity.objects.create(value=validated_data['data']['value'], modified_by=user)
        return entity

    def get_properties(self, obj):
        properties = {}
        for prop in obj.properties.all():
            prop_dict = {'key': prop.key, 'value': prop.value}
            properties[prop_dict['key']] = prop_dict['value']
        return properties