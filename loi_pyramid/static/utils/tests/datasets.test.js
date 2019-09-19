import mockFetch from '../../test_utils/mockFetch.js';
import Datasets from '../datasets.js';

test('new Dataset()', () => {
	const mockDataset = new Datasets.Dataset(
		'mock',
		function () {}
		);
	expect(mockDataset).toBeTruthy();
	expect(mockDataset.name).toBe('mock')
}); 

import noob_account from './__mocks__/noob_account.json';
import noob_characters from './__mocks__/noob_characters.json';

test('Dataset getData()', async () => {
	jest.spyOn(window, 'fetch').mockImplementation( () => {
    return Promise.resolve({
      ok: true,
      json: () => { 
      	return Promise.resolve(noob_characters)
      }
    })
  })

	let response = await Datasets.accountCharacters.getData(noob_account);
	console.log(response);
	let characters = await response;

	expect(characters).toBeTruthy();
	expect(characters).toBe(noob_characters);

	expect(window.fetch).toHaveBeenCalledTimes(1);
});