from django.urls import path

from . import views
urlpatterns = [

    path('',views.Home,name="home"),
    path('product/<slug>',views.ViewProduct,name="product-view"),
    path('products/',views.AllProducts,name="all-product"),


    # =====================carts ==================================
    path('cart/',views.ViewCart,name="cart"),
    path('add-to-cart/',views.AddToCart,name="add-to-cart"),
    path('remove-to-cart/',views.RemoveFromCart,name="remove-to-cart"),
    path('increase-quantity/',views.IncreaseQuantityCart,name="incerase-quantity"),

    # =========================== checkout =======================
    path('checkout/',views.Checkout,name="checkout"),
    path('handlerequest/',views.HandleRequest,name="handlerequest"),

    # ============================ search ========================
    path('search/',views.Search,name="search"),
    path('filter/',views.Filters,name="filters"),


    #  =========================== category ======================
    path('categories/',views.AllCategories,name="categories"),
    path('category/<str:category>',views.GetProductByCategory,name="view-by-category"),

    path('contact/',views.ContactUs,name="contact-us"),
    path('about/',views.AboutUs,name="about-us"),

    # ========================= admin action buttons ============
    path('add-product/',views.AddProduct,name="add-product"),
    path('edit-product/<str:id>',views.EditProduct,name="edit-product"),
    path('product-list/',views.ProductList,name="product-list"),
    path('product-list-filter/',views.FilterProductList,name="product-list-filter"),
    path('product-delete/<str:id>/',views.DeleteProduct,name="product-delete"),
    path('add-category/',views.AddCategory,name="add-categiry"),
    path('update-category/<str:id>',views.EditCategory,name="update-categiry"),
    path('delete-category/<str:id>',views.DeleteCategory,name="delete-categiry"),

    # ======================= auth urls ========================
    path('login/',views.LoginView,name="login"),
    path('logout/',views.LogoutView,name="logout"),
    path('register/',views.Register,name="register"),
    path('verify-otp/',views.VerifyOtp,name="verifyotp"),
    path('recent-otp/',views.RecentOtp,name="resent-otp"),
    path('dashboard/',views.DashBoard,name="DashBoard"),
    path('edit-profile/',views.EditProfile,name="edit-profile"),
    path('dashboard/order/<str:id>',views.EachBookingDetails,name="booking-details"),
    path('generate-pdf/<str:id>',views.GeneratePdf,name="generate-pdf"),
    path('return-request/',views.ReturnReuqest,name="return-request"),



    # ========================== Payment ======================================
]