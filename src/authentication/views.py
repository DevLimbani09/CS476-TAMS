from django.shortcuts import render


def login_page(request):
    if request.method == "POST":
        return render(
            request,
            "login.html",
            {
                "login_error": (
                    "Sign-in functionality is not connected yet."
                )
            },
            status=501,
        )

    return render(request, "login.html")