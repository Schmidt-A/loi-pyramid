import { Dataset } from '../../datasets.js'

const mockDataset = new Dataset(
  'mock',
  jest.fn(mock => {
    return new Promise((resolve, reject) => {
      resolve(new Promise((resolve, reject) => {
        resolve(mock)
      }))
    })
  })
)

export default mockDataset
