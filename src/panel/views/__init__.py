from .analytics import JsonAPI,download_dataset,analytics

from .authentication import LoginView,logout,UserVerifyView

from .dashboard import (
    dashboard,
    EditOrders,
    approve_order,
    reject_order,
    take_responsibility,
    deliver_order,
    pay_order,
)
