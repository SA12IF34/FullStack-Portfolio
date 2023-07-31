let title = document.head.querySelector("title");
let subjectName = document.querySelector("h1");
let booksList = document.querySelector(".booksList ul");

async function getData() {
    let href = window.location.href.split("/")
    let subject = href[href.length-2];
    
    let res = await fetch('/projects/web-scraping/subject-'+subject+'/');
    let data = await res.json();
    
    title.textContent = 'Subject | '+data['subject'];
    subjectName.textContent = data['subject'];
    
    for (var i=0; i < data['data'].length; i++) {
        var li = document.createElement("li");
        var div = document.createElement("div");
        var img = document.createElement("img");
        var h3 = document.createElement("h3");
        var h4 = document.createElement("h4");
        
        li.classList.add('bookItem');

        img.src = data['data'][i]['cover'];
        h3.textContent = data['data'][i]['title'];
        h4.textContent = "By "+data['data'][i]['author'];
        div.append(h3, h4);
        li.append(img,div)

        booksList.appendChild(li);

    }
}

window.onload = () => {
    getData()
}