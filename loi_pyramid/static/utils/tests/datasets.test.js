import { mockDataset, mockRetrieve } from './__mocks__/datasets.js'

const mockData1 = { mockKey: 1 }
const mockData2 = { mockKey: 2 }

beforeEach(() => {
  sessionStorage.clear()
})

test('dataset()', async () => {
  expect(mockDataset).toBeTruthy()

  // verify that we don't have access to these private methods
  expect(mockDataset.name).toBeFalsy()
  expect(mockDataset.retrieve).toBeFalsy()

  expect(mockDataset.attrs().name).toBe('mock')
  expect(mockDataset.attrs().retrieve).toBe(mockRetrieve)
})

test('getData() sessionData', async () => {
  const getData = await mockDataset.getData(mockData2)
  expect(getData.mockKey).toBe(mockData2.mockKey)

  const getDataAgain = await mockDataset.getData(mockData2)
  expect(getDataAgain.mockKey).toBe(mockData2.mockKey)

  // it was cached in session after first
  expect(mockRetrieve).toHaveBeenCalledTimes(1)
})

test('getData() clear()', async () => {
  const getData = await mockDataset.getData(mockData1)
  expect(getData.mockKey).toBe(mockData1.mockKey)

  mockDataset.clear()

  const getDataAgain = await mockDataset.getData(mockData1)
  expect(getDataAgain.mockKey).toBe(mockData1.mockKey)

  expect(mockRetrieve).toHaveBeenCalledTimes(2)
})
