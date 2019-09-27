import Template from '../utils/templates.js'
import loginForm from './login_form.js'

const markup =
  '<div id="login"></div>'

const templateMap = {
  login: loginForm
}

const loginPage = new Template.Page(
  'login',
  markup,
  templateMap
)

export default loginPage
