import mockFetch from '../../utils/mockFetch.js';
import accountData from '../account.js';
import noob_account from './__mocks__/noob_account.json';

test('account retrieve()', async () => {
    jest.spyOn(window, 'fetch').mockImplementation( () => { return mockFetch(true, 200, noob_account) });

    let characters = await accountData.retrieve(noob_account.username);

    expect(characters).toBeTruthy();
    expect(characters).toBe(noob_account);
    expect(window.fetch.mock.calls[0][0]).toBe(`http://sundred.com:6543/accounts/${noob_account.username}`);
});