import Templates from '../utils/templates.js';
import parseResponse from '../utils/xhr.js';

const markup = 
	`<form>
		<label for="user">Username</label> 
		<input type="text" name="user"></input>
		<label for="pw">Password</label>
		<input type="password" name="pw"></input>
		<input type="submit"></input>
	</form>`;

const loginForm = new Templates.Template(
  null,
  markup,
  function () {},
  [new Templates.Listener(
  	'form',
  	'submit',
  	function (event) {
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
          window.dispatchEvent(new Event('triggerPage'));
        })
      })
      .catch(error => {
      })
  	}
  )]);
export default loginForm;