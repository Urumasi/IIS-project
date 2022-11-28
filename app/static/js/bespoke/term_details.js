const APPLY_LOADING = '<i class="fa fa-spinner"></i> Apply';
const APPLY_SUCCESS = '<i class="fa fa-check-circle"></i> Apply';
const APPLY_FAIL = '<i class="fa fa-check-times"></i> Apply';

function send_point_update(button, user_id, term, points) {
    console.log(button, user_id, term, points);
    button.innerHTML = APPLY_LOADING;
    const xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if(this.readyState == XMLHttpRequest.DONE && this.status == 200) {
            let result = JSON.parse(this.responseText);
            console.log(result);
            if(result.status == "success") {
                button.innerHTML = APPLY_SUCCESS;
            } else {
                button.innerHTML = APPLY_FAIL;
            }
            button.busy = false;
        }
    }
    xhttp.open("POST", "/api/change_points", true);
    xhttp.setRequestHeader("Content-Type", "application/json");
    let data = {
        'user': user_id,
        'term': term,
        'points': points
    };
    xhttp.send(JSON.stringify(data));
}

function apply_points(self, user_id, term) {
    let input = self.parentNode.parentNode.children[1].children[0];
    console.log(self);
    if (input.value === '') {
        console.log('Empty');
        return;
    }
    if (self.busy === true) {
        console.log('Busy');
        return;
    }
    self.busy = true;
    send_point_update(self, user_id, term, input.value);
}
