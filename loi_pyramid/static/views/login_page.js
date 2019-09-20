import Template from '../utils/templates.js';
import loginForm from './login_form.js';

let markup = 
  `<div id="login"></div>`;

let templateMap = {
  'login': loginForm
};
  
let logout = function () {
  let account = sessionStorage.getItem('account');
  fetch('http://sundred.com:6543/logout')
  .then(response => {
    console.log(`logged out of ${account.id}`);
    sessionStorage.removeItem('account')
  })
  .catch(response => {})
}

const loginPage = new Template.Page(
  document.querySelector('#pageContainer'),
  'login',
  markup,
  templateMap
);

export default loginPage;