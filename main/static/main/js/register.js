function visibilityPassword() {

    let passwordCheckButton = document.getElementById('passwordCheckButton');
    let visibility = document.getElementById('visibility_check_password');
    let unvisibility = document.getElementById('unvisibility_check_password');
    let visibilityTest = false;

    let inputPassword = document.getElementById('input_password');

    passwordCheckButton.addEventListener('click', () => {
        if (visibilityTest) {
            visibilityTest = false;
            visibility.style.display = 'block';
            unvisibility.style.display = 'none';

            inputPassword.type = 'text';

        }
        else {
            visibilityTest = true;
            unvisibility.style.display = 'block';
            visibility.style.display = 'none';

            inputPassword.type = 'password';
        }
    })

}

visibilityPassword();

let passwordInput = document.querySelector('#input_password');
let dropdownMenus = document.querySelectorAll('.dragdown_block_check_password');

function checkPassword() {
    let validateTest;
    let checkbox = document.getElementById('checkbox_accept_sign-up');
    let checkedBox = document.getElementById('checkedBox');
    let submitButton = document.getElementById('submit_button');
    let test = false;
    let inputRepeatPassword = document.getElementById('input_repeat_password').value;

    inputRepeatPassword = inputRepeatPassword.trim();
    document.getElementById('input_repeat_password').value = inputRepeatPassword;
    let password = passwordInput.value;

    let conditions = [
        password.length >= 8,
        /\d/.test(password),
        /[a-z]/i.test(password),
        /\W/.test(password)
    ];

    dropdownMenus.forEach(function(menu) {
        menu.classList.remove('active');
    });

    let conditionCount = 0;

    for (let i = 0; i < conditions.length; i++) {
        if (conditions[i]) {
            if (conditionCount < dropdownMenus.length) {
                dropdownMenus[conditionCount].classList.add('active');
                conditionCount++;
            }
        }
    }

    if (conditionCount === 4 && password === inputRepeatPassword) {
        validateTest = true;
        test = true;
    }
    else {
        validateTest = false;
    }

    if(test) {
        test = true;
        checkbox.style.display = "block";
        submitButton.style.marginTop = "30px";
    }
    else {
        test = false;
        checkbox.style.display = "none";
        submitButton.style.marginTop = "30px";
    }

    if(checkedBox.checked) {
        submitButton.disabled = false;
        submitButton.style.backgroundColor = "#0096FF";
        submitButton.style.cursor = "pointer";
    }
    else if(!checkedBox.checked) {
        submitButton.disabled = true;
        submitButton.style.backgroundColor = "#5e6778";
        submitButton.style.cursor = "default";
    }

}

checkPassword();
