import mockFetch from '../../utils/mockFetch.js';
import accountCharactersData from '../account_characters.js';
import noob_account from './__mocks__/noob_account.json';
import noob_characters from './__mocks__/noob_characters.json';

//these tests are kinda useless
test('accountCharacters retrieve()', async () => {
    jest.spyOn(window, 'fetch').mockImplementation( () => { return mockFetch(true, 200, noob_characters) });

    let characters = await accountCharactersData.retrieve(noob_account);

    expect(characters).toBeTruthy();
    expect(characters).toBe(noob_characters);
    expect(window.fetch.mock.calls[0][0]).toBe(`http://sundred.com:6543/accounts/${noob_account.username}/characters`);
});