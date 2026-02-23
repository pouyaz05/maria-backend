from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.core.mail import send_mail
from django.conf import settings

import json
import re
import logging
from threading import Thread

from .models import Order, Painting

logger = logging.getLogger(__name__)


# ==================== توابع کمکی ====================

def normalize_phone(phone):
    phone = re.sub(r'\D', '', phone)
    if phone.startswith('0'):
        phone = '98' + phone[1:]
    elif not phone.startswith('98'):
        phone = '98' + phone
    return phone


# ==================== ثبت سفارش (بدون painting_id) ====================

class OrderCreateView(View):

    @method_decorator(csrf_exempt)
    @method_decorator(require_POST)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    @transaction.atomic
    def post(self, request):
        try:
            data = json.loads(request.body.decode("utf-8"))

            name = data.get("customer_name", "").strip()
            phone = data.get("customer_phone", "").strip()
            description = data.get("custom_message", "").strip()

            # فقط این دو تا اجباری
            if not name or not phone:
                return JsonResponse(
                    {"error": "نام و شماره تماس الزامی است"},
                    status=400
                )

            # اعتبارسنجی شماره موبایل ایرانی
            if not re.match(r'^09\d{9}$', phone):
                return JsonResponse(
                    {"error": "شماره تلفن معتبر نیست"},
                    status=400
                )

            # ساخت سفارش (دیگه هیچ ارتباطی با Painting نداره)
            order = Order.objects.create(
                customer_name=name,
                customer_phone=normalize_phone(phone),
                customer_description=description
            )

            # ارسال ایمیل در بک‌گراند
            Thread(target=self.send_email, args=(order,)).start()

            return JsonResponse({
                "success": True,
                "message": "درخواست شما با موفقیت ثبت شد",
                "order_id": order.id
            }, status=201)

        except Exception as e:
            logger.error(str(e))
            return JsonResponse(
                {"error": "خطای سرور"},
                status=500
            )

    def send_email(self, order):
        try:
            subject = "درخواست جدید ثبت شد"

            message = f"""
درخواست جدید ثبت شد:

نام مشتری: {order.customer_name}
شماره تماس: {order.customer_phone}
توضیحات: {order.customer_description}
"""

            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [settings.ADMIN_EMAIL],
                fail_silently=True,
            )

        except Exception as e:
            logger.error(f"Email error: {str(e)}")


# ==================== لیست سفارش‌ها (فقط ادمین) ====================

@method_decorator(login_required, name="dispatch")
class OrderListView(View):
    def get(self, request):
        if not request.user.is_staff:
            return JsonResponse({"error": "دسترسی غیرمجاز"}, status=403)

        orders = Order.objects.order_by("-created_at")[:50]

        data = [{
            "id": o.id,
            "customer_name": o.customer_name,
            "customer_phone": o.customer_phone,
            "description": o.customer_description,
            "created_at": o.created_at.isoformat(),
        } for o in orders]

        return JsonResponse({"orders": data})


# ==================== API آثار ====================

def painting_list_api(request):
    paintings = Painting.objects.filter(is_available=True).order_by("-id")

    data = [{
        "id": p.id,
        "title": p.title,
        "artist_name": p.artist_name,
        "description": p.description,
        "year": p.year_created,
        "image": request.build_absolute_uri(p.image.url) if p.image else None,
    } for p in paintings]

    return JsonResponse(data, safe=False)
