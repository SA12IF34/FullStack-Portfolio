let container = document.querySelector(".skills>div");

let frontendContainer = document.querySelector('.frontend');
let backendContainer = document.querySelector('.backend');

let frontendSkills = document.querySelectorAll(".frontend span");
let backendSkills = document.querySelectorAll(".backend span");

let locations1 = [
    [70, 70],    // [ X , Y ]
    [50, 50], 
    [20, 70],
    [30, 60],
    [45, 90],
    [40, 10], 
    [80, 45],
    [50, 30]
    
];
let locations2 = [
    [20, 40],    // [ X , Y ]
    [15, 60], 
    [30, 80],
    [35, 35],
    [50, 70],
    [70, 85], 
    [70, 55],
    [80, 40],
    [75, 20]
];


let locationsInstanceOne = [...locations1];



frontendSkills.forEach((skill, index) => {
    let loc = Math.floor(Math.random() * locationsInstanceOne.length)
    
    let x = locationsInstanceOne[loc][0];
    let y = locationsInstanceOne[loc][1];
    
    skill.style.cssText = `left: ${x}%; top: ${y}%;`
    locationsInstanceOne.splice(loc, 1);

    if ((index % 2) === 0) {
        skill.classList.add('even');
        skill.style.transform = 'translateZ(60px)';
    } else {
        skill.classList.add('odd');
        skill.style.transform = 'translateZ(-30px)';
    }

})

let locationsInstanceTwo = [...locations2];



backendSkills.forEach((skill, index) => {
    let loc = Math.floor(Math.random() * locationsInstanceTwo.length)
    
    let x = locationsInstanceTwo[loc][0];
    let y = locationsInstanceTwo[loc][1];
    
    skill.style.cssText = `left: ${x}%; top: ${y}%;`
    locationsInstanceTwo.splice(loc, 1);

    if ((index % 2) === 0) {
        skill.classList.add('even');
        skill.style.transform = 'translateZ(60px)';
    } else {
        skill.classList.add('odd');
        skill.style.transform = 'translateZ(-30px)';
    }

})

function getOffset( el ) {
    var _x = 0;
    var _y = 0;
    while( el && !isNaN( el.offsetLeft ) && !isNaN( el.offsetTop ) ) {
        _x += el.offsetLeft - el.scrollLeft;
        _y += el.offsetTop - el.scrollTop;
        el = el.offsetParent;
    }
    return { top: _y, left: _x };
}


backendContainer.addEventListener('mousemove', (e) => {

    backendSkills.forEach(skill => {
        var rect = skill.getBoundingClientRect();
        if ((rect.x+50 >= e.clientX && rect.x-50 <= e.clientX )|| (rect.y+50 >= e.clientY && rect.y-50 <= e.clientY)) {
            skill.classList.add('hover')
        } else {
            skill.classList.remove('hover');
        }   
    })
})

frontendContainer.addEventListener('mousemove', (e) => {

    frontendSkills.forEach(skill => {
        var rect = skill.getBoundingClientRect();
        if ((rect.x+50 >= e.clientX && rect.x-50 <= e.clientX )|| (rect.y+50 >= e.clientY && rect.y-50 <= e.clientY)) {
            skill.classList.add('hover')
        } else {
            skill.classList.remove('hover');
        }   
    })
})