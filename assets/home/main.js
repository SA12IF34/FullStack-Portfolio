window.onload = () => {
    let welcome = document.querySelector('#welcome');
    welcome.classList.add('welcome');
    welcome.classList.remove('not-welcome');

    let leftParagraphs = document.querySelectorAll('#left');
    let rightParagraphs = document.querySelectorAll('#right')

    let leftObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('left');
                entry.target.classList.remove('left-hide');
                observer.unobserve(entry.target);
            }
        })
    })

    let rightObserver = new IntersectionObserver((entries, observer) => {
        
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                
                entry.target.classList.add('right');
                entry.target.classList.remove('right-hide');
                observer.unobserve(entry.target);
            }
        })
    })

    setTimeout(() => {
        leftParagraphs.forEach(lp => {
            leftObserver.observe(lp);
        })
    
        rightParagraphs.forEach(rp => {
            rightObserver.observe(rp);
        })
    }, 1100)
}