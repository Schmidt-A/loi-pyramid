import mockFetch from '../../test_utils/mockFetch.js';
import Datasets from '../datasets.js';

test('new Dataset()', async () => {
	const mockDataset = new Datasets.Dataset(
		'mock',
		jest.fn().mockImplementation( mock => {
			return Promise.resolve(mock)
		}));
	expect(mockDataset).toBeTruthy();
	expect(mockDataset.name).toBe('mock');
	expect(await mockDataset.retrieve('mock')).toBe('mock');
	expect(await mockDataset.getData('mock')).toBe('mock');
});

test('getData() sessionData', async () => {
	const mockDataset = new Datasets.Dataset(
		'mock',
		function (mock) { return Promise.resolve( mock ) }
		);

	let mockData = {'mockKey': 'mockValue'};
	sessionStorage.setItem('mock', JSON.stringify(mockData));

	expect(mockDataset).toBeTruthy();
	expect(await mockDataset.retrieve('mock')).toBe('mock');

	let mockResponse = await mockDataset.getData('mock');
	expect(mockResponse.mockKey).toBe(mockData.mockKey);
});

import noob_account from './__mocks__/noob_account.json';
import noob_characters from './__mocks__/noob_characters.json';

test('account retrieve()', async () => {
	jest.spyOn(window, 'fetch').mockImplementation( () => { return mockFetch(noob_account) });

	let characters = await Datasets.account.retrieve(noob_account.username);

	expect(characters).toBeTruthy();
	expect(characters).toBe(noob_account);
	expect(window.fetch.mock.calls[0][0]).toBe(`http://sundred.com:6543/accounts/${noob_account.username}`);
});

test('accountCharacters retrieve()', async () => {
	jest.spyOn(window, 'fetch').mockImplementation( () => { return mockFetch(noob_characters) });

	let characters = await Datasets.accountCharacters.retrieve(noob_account);

	expect(characters).toBeTruthy();
	expect(characters).toBe(noob_characters);
	expect(window.fetch.mock.calls[0][0]).toBe(`http://sundred.com:6543/accounts/${noob_account.username}/characters`);
});