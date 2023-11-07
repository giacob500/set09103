window.addEventListener('DOMContentLoaded', (event) => {
    var counter = 0;
    var counterElement = document.getElementById('counter');
    var cells = document.getElementsByTagName('td');
    var selectedList = document.getElementById('selectedList');
    
    for (var i = 0; i < cells.length; i++) {
        cells[i].addEventListener('click', function() {
            if (!this.classList.contains('selected')) {
                counter++;
                counterElement.innerText = counter;
                this.classList.add('selected');
                this.classList.add('clicked');
                
                var cellText = this.innerText;
                var listItem = document.createElement('li');
                listItem.innerText = cellText;
                selectedList.appendChild(listItem);
            } else {
                counter--;
                counterElement.innerText = counter;
                this.classList.remove('selected');
                this.classList.remove('clicked');
                
                var cellText = this.innerText;
                var listItems = selectedList.getElementsByTagName('li');
                for (var j = 0; j < listItems.length; j++) {
                    if (listItems[j].innerText === cellText) {
                        selectedList.removeChild(listItems[j]);
                        break;
                    }
                }
            }
        });
    }
});

// This is for the Quantity selector in /product page
