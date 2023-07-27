// navabr position
let navbar = document.querySelector(".navbar-azma")
window.addEventListener("scroll", (e)=>{
    if (window.scrollY <= 5)
    {
        navbar.classList.add("py-3")
        navbar.classList.remove("navbar-bg-normal")
        navbar.classList.add("navbar-bg-dark")
    }
    else{
        navbar.classList.remove("py-3")
        navbar.classList.add("navbar-bg-normal")
        navbar.classList.remove("navbar-bg-dark")
    }
})