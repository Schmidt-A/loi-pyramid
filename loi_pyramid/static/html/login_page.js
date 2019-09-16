import Template from '../js/template.js';
import loginForm from './login_form.js';

let loginPageMarkup = 
  `<div id="login"></div>`;

let loginTemplateMap = {
  'login': loginForm
}
  
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
  'login',
  logout,
  loginPageMarkup,
  loginTemplateMap,
  function () {
    loginForm.afterRender();
  });

export default loginPage;