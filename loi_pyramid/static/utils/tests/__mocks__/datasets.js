import Datasets from '../../datasets.js';

const mockDataset = new Datasets.Dataset(
    'mock',
    jest.fn( mock => {
        return Promise.resolve(mock)
    })
);

export default mockDataset;