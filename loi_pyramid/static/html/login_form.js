import Template from '../js/template.js';

const loginFormMarkup = 
	`<form>
		<label for="user">Username</label> 
		<input type="text" name="user"></input>
		<label for="pw">Password</label>
		<input type="password" name="pw"></input>
		<input type="submit"></input>
	</form>`;

const loginForm = new Template.Content(
  function () {},
  loginFormMarkup,
  function () {
    let form = document.querySelector(`#${this.container.id} form`);
    form.addEventListener('submit', event => {
      event.preventDefault();
      let formData = new FormData(event.srcElement);
      fetch('http://sundred.com:6543/login', {
        method: 'POST',
        body: formData
      })
      .then(response => {
        parseResponse(response).then( account => {
          sessionStorage.setItem('account', JSON.stringify(account));
          console.log(JSON.stringify(account));
        })
      })
      .catch(error => {
      })
    })
  });
export default loginForm;