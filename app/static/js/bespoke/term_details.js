const APPLY_LOADING = '<i class="fa fa-spinner"></i> Apply';
const APPLY_SUCCESS = '<i class="fa fa-check-circle"></i> Apply';
const APPLY_FAIL = '<i class="fa fa-check-times"></i> Apply';

function apply_points(self) {
    let input = self.parentNode.parentNode.children[1].children[0];
    if (input.value === '') {
        return;
    }
    if (self.busy) {
        return;
    }
    console.log("Click");
    self.busy = true;
    self.innerHTML = APPLY_LOADING;

}
