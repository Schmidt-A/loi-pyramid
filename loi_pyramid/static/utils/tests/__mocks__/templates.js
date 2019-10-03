import templates from '../../templates.js'

// the practice of using the dom for these unit mocks is possibly problematic
const mockContentContainer = document.createElement('div')
mockContentContainer.id = 'contentContainer'
document.body.appendChild(mockContentContainer)

export const mockEventFunction = jest.fn(event => {
  event.preventDefault()
})

export const mockListener = templates.listener(
  'div',
  'focus',
  mockEventFunction
)

export const mockTemplate = {
  markup: '<div class="mock"></div>',
  listeners: [mockListener],
  dataset: jest.mock('../../datasets.js'),
  renderData: jest.fn(() => { return Promise.resolve() })
}

export const mockPage = templates.page(
  'mock',
  '<div id="sampleContent"></div>',
  { sampleContent: mockTemplate }
)
