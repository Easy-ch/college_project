const buttons = document.querySelectorAll('button');

buttons.forEach(button => {
    button.addEventListener('click', () => {
        button.classList.add('active');

        setTimeout(() => {button.classList.add('active');}, 0);

        setTimeout(() => {button.classList.remove('active');}, 40);
    });
});


const calalog_grid_item = document.querySelectorAll('.calalog-grid-item');

function fadeInRight() {
    calalog_grid_item.forEach((GridItem, i) => {
        setTimeout(() => {
            GridItem.classList.add('active');
        }, i * 200);
    });
}

document.addEventListener('DOMContentLoaded', fadeInRight());