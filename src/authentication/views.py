from django.shortcuts import render

# Create your views here.

def login_page(request):
    if request.method == "POST":
        return render(
            request,
            "authentication/login.html",
            {
                "login_error": (
                    "Sign-in functionality is not connected yet."
                )
            },
            status=501,
        )

    return render(request, "authentication/login.html")
