module "ecr_front" {
  source       = "./modules/ecr"
  project_name = "${local.project_name}-front"
}

module "ecr_back" {
  source       = "./modules/ecr"
  project_name = "${local.project_name}-back"
}

module "ecr_crawler" {
  source       = "./modules/ecr"
  project_name = "${local.project_name}-crawler"
}

module "ecr_train_model" {
  source       = "./modules/ecr"
  project_name = "${local.project_name}-train-model"
}