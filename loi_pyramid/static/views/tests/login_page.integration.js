import Templates from '../../utils/templates.js';
import mockFetch from '../../utils/mock_fetch.js';
import loginPage from '../login_page.js';
import accountData from '../../models/account.js';
import noobAccount from '../../models/tests/__mocks__/noob_account.json';

let pageContainer = document.createElement('div');
pageContainer.id = 'pageContainer';
document.body.appendChild(pageContainer);
loginPage.container = document.querySelector('#pageContainer');

beforeEach( () => {
    sessionStorage.clear();
    loginPage.container.innerHTML = '';
    expect(loginPage.container.children.length).toBe(0);
});

test('Page render()', async () => {
	jest.spyOn(window, 'fetch').mockImplementation( () => { return mockFetch(true, 200, noobAccount) });

    await loginPage.render();

    expect(window.location.pathname).toBe('/app/login');

    //this indicates that these form fields have no value
    expect(() => { new FormData(loginPage.contentMap.login)}).toThrow();

	document.querySelector("#login input[name='user']").value = noobAccount.username;
	document.querySelector("#login input[name='pw']").value = 'drizzit4ever';
	document.querySelector("#login input[type='submit']").click();

	expect(window.fetch.mock.calls[0][0]).toBe(`http://sundred.com:6543/login`);
	expect(window.fetch.mock.calls[0][1].method).toBe(`POST`);

	let postData = window.fetch.mock.calls[0][1].body;
	expect(postData.get('user')).toBe(noobAccount.username);
	expect(postData.get('pw')).toBe('drizzit4ever');
	
	expect(await accountData.getData(noobAccount.username)).toEqual(noobAccount);
});