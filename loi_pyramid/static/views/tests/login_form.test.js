import mockFetch from '../../utils/mock_fetch.js';
import loginForm from '../login_form.js';

beforeEach(() => {
    sessionStorage.clear();
});

//this is really about testing that forming of the POST
test('loginForm Listener eventFunction() success', () => {
	jest.spyOn(window, 'fetch').mockImplementation( () => { return mockFetch(true, 200, {}) });

	let markup = 
	`<form>
		<input type="text" name="user" value=mockUsername></input>
		<input type="password" name="pw" value="mockPassword"></input>
	</form>`;
	document.body.innerHTML = markup;

	let mockEvent = {
		srcElement: document.body.children[0],
		preventDefault: () => {}
	};

	loginForm.listeners[0].eventFunction(mockEvent);

	expect(window.fetch.mock.calls[0][0]).toBe(`http://sundred.com:6543/login`);
	expect(window.fetch.mock.calls[0][1].method).toBe(`POST`);

	let data = window.fetch.mock.calls[0][1].body;
	expect(data.get('user')).toBe('mockUsername');
	expect(data.get('pw')).toBe('mockPassword');
});
