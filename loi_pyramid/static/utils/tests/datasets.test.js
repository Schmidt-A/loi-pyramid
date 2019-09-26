import mockDataset from './__mocks__/datasets.js'

const mockData1 = { mockKey: 1 }
const mockData2 = { mockKey: 2 }

beforeEach(() => {
  sessionStorage.clear()
})

test('new Dataset()', async () => {
  expect(mockDataset).toBeTruthy()
  expect(mockDataset.name).toBe('mock')

  const mockRetrieve = await mockDataset.retrieve(mockData1)
  expect(mockRetrieve.mockKey).toBe(mockData1.mockKey)
})

test('getData() retrieve()', async () => {
  const mockRetrieve = await mockDataset.retrieve(mockData1)
  expect(mockRetrieve.mockKey).toBe(mockData1.mockKey)

  const mockGetData = await mockDataset.getData(mockData1)
  expect(mockGetData.mockKey).toBe(mockData1.mockKey)

  expect(mockDataset.retrieve).toHaveBeenCalledTimes(2)
})

test('getData() sessionData', async () => {
  sessionStorage.setItem('mock', JSON.stringify(mockData2))

  const mockGetData = await mockDataset.getData(mockData2)
  expect(mockGetData.mockKey).toBe(mockData2.mockKey)
  expect(mockDataset.retrieve).toHaveBeenCalledTimes(0)
})
