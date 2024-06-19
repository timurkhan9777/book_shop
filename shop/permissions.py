from django.contrib.auth.mixins import AccessMixin

class AdminRequiredMixin(AccessMixin):
    def dispatch(self,request,*args,**kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not request.user.user_role == "admin":
            return self.handle_no_permission()

        return super().dispatch(request,*args,**kwargs)


class SellerRequiredMixin(AccessMixin):
    def dispatch(self,request,*args,**kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not request.user.user_role == "seller" and not request.user.user_role == "admin":
            return self.handle_no_permission()

        return super().dispatch(request,*args,**kwargs)

class ClientRequiredMixin(AccessMixin):
    def dispatch(self,request,*args,**kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not request.user.user_role == "client":
            return self.handle_no_permission()

        return super().dispatch(request,*args,**kwargs)