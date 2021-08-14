function setFormMessage(formElement, type, message) {
    const messageElement = formElement.querySelector(".form__message");

    messageElement.textContent = message;
    messageElement.classList.remove("form__message--success", "form__message--error");
    messageElement.classList.add(`form__message--${type}`);
}

function setInputError(inputElement, message) {
    inputElement.classList.add("form__input--error");
    inputElement.parentElement.querySelector(".form__input-error-message").textContent = message;
}

function clearInputError(inputElement) {
    inputElement.classList.remove("form__input--error");
    inputElement.parentElement.querySelector(".form__input-error-message").textContent = "";
}

document.addEventListener("DOMContentLoaded", () => {
    const loginForm = document.querySelector("#login");
    const createAccountForm = document.querySelector("#createAccount");
    const ForgetPasswordForm = document.querySelector("#ForgetPassword")


    loginForm.addEventListener("submit", e => {

        if ($("#username").val() === "") {
            e.preventDefault();
            setFormMessage(loginForm, "error", "نام کاربری را وارد گنید");
        }
        else if ($("#password").val() === "") {
            e.preventDefault();
            setFormMessage(loginForm, "error", "رمز عبور را وارد گنید");
        }


    });

    createAccountForm.addEventListener("submit", e => {

        if ($("#name").val() === "") {
            e.preventDefault();
            setFormMessage(createAccountForm, "error", "نام خود را وارد کنید");
        }
        else if ($("#lastname").val() === "") {
            e.preventDefault();
            setFormMessage(createAccountForm, "error", "نام خانوداگی خود را وارد کنید");
        }
        else if ($("#signupUsername").val() === "") {
            e.preventDefault();
            setFormMessage(createAccountForm, "error", "نام کاربری را وارد کنید");
        }
        else if ($("#password").val() === "") {
            e.preventDefault();
            setFormMessage(createAccountForm, "error", "رمز عبور را وارد کنید");
        }
        else if ($("#re_password").val() !== $("#re_password").val()) {
            e.preventDefault();
            setFormMessage(createAccountForm, "error", "رمز عبور با تکرار آن تطابق ندارد");
        }


    });

    document.querySelectorAll(".form__input").forEach(inputElement => {
        inputElement.addEventListener("blur", e => {
            if (e.target.id === "signupUsername" && e.target.value.length > 0 && e.target.value.length < 5) {
                setInputError(inputElement, "نام کاربری باید حداقل 5 حرف باشد");
            }
        }); 

        inputElement.addEventListener("input", e => {
            clearInputError(inputElement);
        });
    });
    $("form").on("change", ".file-upload-field", function(){
    $(this).parent(".file-upload-wrapper").attr("data-text",         $(this).val().replace(/.*(\/|\\)/, '') );
});
});