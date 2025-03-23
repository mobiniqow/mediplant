from rest_framework import serializers
from .models import Ticket, Message, TicketSection


class TicketSerializer(serializers.ModelSerializer):
    messages = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Ticket
        fields = ('id', 'title', 'state','messages')
        read_only_fields = ('state',)

    def create(self, validated_data):
        user = self.context['request'].user
        return super().create({**validated_data, "user": user})

    def get_messages(self, obj):
        messages = obj.messages.all().order_by('timestamp')
        return MessageSerializer(messages, many=True).data


class TicketSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketSection
        fields = "__all__"


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('text', 'file','is_user')
        read_only_fields = ('is_user',)

    def create(self, validated_data):
        ticket_id = self.context['view'].kwargs.get('ticket_id')  # بررسی مقدار ticket_id
        user = self.context['request'].user  # دریافت کاربر ارسال‌کننده

        # بررسی اینکه ticket_id معتبر باشد
        try:
            ticket = Ticket.objects.get(id=ticket_id)
        except Ticket.DoesNotExist:
            raise serializers.ValidationError({"ticket": "Ticket not found."})

        # ایجاد و بازگرداندن نمونه جدید
        message = Message.objects.create(
            ticket=ticket,
            message_sender=user,
            text=validated_data.get("text", ""),  # مقدار پیش‌فرض برای جلوگیری از خطا
            file=validated_data.get("file", None)
        )
        return message
