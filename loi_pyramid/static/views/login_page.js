import Template from '../utils/templates.js';
import loginForm from './login_form.js';

let markup = 
  `<div id="login"></div>`;

let templateMap = {
  'login': loginForm
};

const loginPage = new Template.Page(
  'login',
  markup,
  templateMap
);

export default loginPage;