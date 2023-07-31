
let trending = document.querySelector(".trending");
let trendingList = document.querySelector(".trending ul");
let subjectsList = document.querySelector(".subjects ul");


async function getBooks() {
    let res = await fetch('/projects/web-scraping/books/trending/');
    let data = await res.json();

    for (var i=0; i < data['data'].length; i++) {
        var li = document.createElement("li");
        var img = document.createElement("img");
        var p = document.createElement("p");
        
        li.classList.add("book");

        img.src = data['data'][i]['img'];
        img.setAttribute("data-", data['data'][i]['img'])
        p.textContent = data['data'][i]['name'];
        li.append(img, p);
        trendingList.appendChild(li);
    }
}

async function getSubjects() {
    let res = await fetch('/projects/web-scraping/subjects/');
    let data = await res.json();

    for (var i=0; i < data['data'].length; i++) {
        var li = document.createElement("li");
        var a = document.createElement("a");

        a.textContent = data['data'][i];
        a.href = "/projects/web-scraping"+data['urls'][i]+"/";

        li.appendChild(a);
        subjectsList.appendChild(li);

        li.onclick = () => {
            window.sessionStorage.setItem('subject',data['data'][i])
        }
    };
}

window.onload = () => {
    getBooks();
    getSubjects();
}