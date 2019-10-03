import { dataset } from '../../datasets.js'

export const mockRetrieve = jest.fn(mock => {
  return new Promise((resolve, reject) => {
    resolve(new Promise((resolve, reject) => {
      resolve(mock)
    }))
  })
})

export const mockDataset = dataset(
  'mock',
  mockRetrieve
)
