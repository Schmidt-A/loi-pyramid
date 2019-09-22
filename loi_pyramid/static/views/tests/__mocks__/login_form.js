import Templates from '../../../utils/templates.js';
import loginForm from '../../login_form.js';

const testLoginForm = new Templates.Template( 
    loginForm.dataset,
    loginForm.markup,
    loginForm.renderData,
    [new Templates.Listener(
        'form',
        'submit',
        function (event) {
            event.preventDefault();
            //put verification logic in here
        }
    )]
);

export default testLoginForm;