// Change the color of a navbar link according to the current url 

href = window.location.href

navbarLinks = document.querySelectorAll('.nav-link')

for (link of navbarLinks) {
    if (href == link.href) {
        link.style = "color: white;"
    }
}