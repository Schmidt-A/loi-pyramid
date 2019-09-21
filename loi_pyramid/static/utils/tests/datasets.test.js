import mockFetch from '../../test_utils/mockFetch.js';
import Datasets from '../datasets.js';
import mockDataset from './__mocks__/datasets.js';

let mockData1 = {'mockKey': 1};
let mockData2 = {'mockKey': 2};

test('new Dataset()', async () => {
    expect(mockDataset).toBeTruthy();
    expect(mockDataset.name).toBe('mock');

    let mockRetrieve = await mockDataset.retrieve(mockData1)
    expect(mockRetrieve.mockKey).toBe(mockData1.mockKey);
});

test('getData() retrieve()', async () => {
    let mockRetrieve = await mockDataset.retrieve(mockData1)
    expect(mockRetrieve.mockKey).toBe(mockData1.mockKey);

    let mockGetData = await mockDataset.getData(mockData1)
    expect(mockGetData.mockKey).toBe(mockData1.mockKey);

    expect(mockDataset.retrieve).toHaveBeenCalledTimes(2);
});

test('getData() sessionData', async () => {
    sessionStorage.setItem('mock', JSON.stringify(mockData2));

    let mockGetData = await mockDataset.getData(mockData2);
    expect(mockGetData.mockKey).toBe(mockData2.mockKey);
    expect(mockDataset.retrieve).toHaveBeenCalledTimes(0);
});

import noob_account from './__mocks__/noob_account.json';
import noob_characters from './__mocks__/noob_characters.json';

test('account retrieve()', async () => {
    jest.spyOn(window, 'fetch').mockImplementation( () => { return mockFetch(true, 200, noob_account) });

    let characters = await Datasets.account.retrieve(noob_account.username);

    expect(characters).toBeTruthy();
    expect(characters).toBe(noob_account);
    expect(window.fetch.mock.calls[0][0]).toBe(`http://sundred.com:6543/accounts/${noob_account.username}`);
});

test('accountCharacters retrieve()', async () => {
    jest.spyOn(window, 'fetch').mockImplementation( () => { return mockFetch(true, 200, noob_characters) });

    let characters = await Datasets.accountCharacters.retrieve(noob_account);

    expect(characters).toBeTruthy();
    expect(characters).toBe(noob_characters);
    expect(window.fetch.mock.calls[0][0]).toBe(`http://sundred.com:6543/accounts/${noob_account.username}/characters`);
});