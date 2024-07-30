Rails.application.routes.draw do
  devise_for :users, controllers: { registrations: 'registrations', sessions: 'sessions' }
  resources :users, only: [:index, :show]
  root 'home#index'
  resources :deputies, only: [:index, :show]
  resources :search, only: [:index, :show]
end
