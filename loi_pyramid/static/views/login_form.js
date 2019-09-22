import Templates from '../utils/templates.js';

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
      let fetchRetrieve = fetch('http://sundred.com:6543/login', {
        method: 'POST',
        body: formData
      })
      .then( response => {
        return response.json()
      })
      .then( account => {
        sessionStorage.setItem('account', JSON.stringify(account));
        console.log(JSON.stringify(account));
        window.dispatchEvent(new Event('triggerPage'));
      })
      .catch( error => {
      })
  	}
  )]
);
export default loginForm;