import { Dataset } from '../datasets.js';
import mockDataset from './__mocks__/datasets.js';

let mockData1 = {'mockKey': 1};
let mockData2 = {'mockKey': 2};

test('new Dataset()', async () => {
    expect(mockDataset).toBeTruthy();
    expect(mockDataset.name).toBe('mock');

    let mockRetrieve = await mockDataset.retrieve(mockData1);
    expect(mockRetrieve.mockKey).toBe(mockData1.mockKey);
});

test('getData() retrieve()', async () => {
    let mockRetrieve = await mockDataset.retrieve(mockData1);
    expect(mockRetrieve.mockKey).toBe(mockData1.mockKey);

    let mockGetData = await mockDataset.getData(mockData1);
    expect(mockGetData.mockKey).toBe(mockData1.mockKey); 

    expect(mockDataset.retrieve).toHaveBeenCalledTimes(2);
});

test('getData() sessionData', async () => {
    sessionStorage.setItem('mock', JSON.stringify(mockData2));

    let mockGetData = await mockDataset.getData(mockData2);
    expect(mockGetData.mockKey).toBe(mockData2.mockKey);
    expect(mockDataset.retrieve).toHaveBeenCalledTimes(0);
});


