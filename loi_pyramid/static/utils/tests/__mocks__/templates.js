import Templates from '../../templates.js'

// the practice of using the dom for these unit mocks is possibly problematic
const mockPageContainer = document.createElement('div')
mockPageContainer.id = 'pageContainer'
document.body.appendChild(mockPageContainer)
const mockContentContainer = document.createElement('div')
mockContentContainer.id = 'contentContainer'
document.body.appendChild(mockContentContainer)

export const mockListener = new Templates.Listener(
  'div',
  'focus',
  jest.fn(event => {
    event.preventDefault()
  })
)

export const mockTemplate = new Templates.Template(
  jest.mock('../../datasets.js'),
  '<div class="mock"></div>',
  jest.fn(() => { return Promise.resolve() }),
  [mockListener]
)

export const mockContent = new Templates.Content(
  mockTemplate.dataset,
  mockTemplate.markup,
  mockTemplate.renderData,
  mockTemplate.listeners,
  mockContentContainer
)

export const mockPage = new Templates.Page(
  'mock',
  '<div id="sampleContent"></div>',
  { sampleContent: mockTemplate },
  mockPageContainer
)
