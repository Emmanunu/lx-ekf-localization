#!/usr/bin/env python3

import numpy as np
from multiprocessing import Lock


def wrap_angle(a):
    """Wrap angle to [-pi, pi]."""
    return (a + np.pi) % (2*np.pi) - np.pi

class EKF:
    def __init__(self, q_0: np.ndarray, P_0: np.ndarray, Q: np.ndarray, R: np.ndarray):
        self.q = q_0
        self.P = P_0
        self.Q = Q
        self.R = R
        self.q_mutex = Lock()

    def predict(self, dX, dT):

        with self.q_mutex:

            # Étape 1 : mettre à jour l'estimation de la pose à l'aide du modèle cinématique
            # TODO: à faire
            self.q[0] = self.q[0]
            self.q[1] = self.q[1]
            self.q[2] = self.q[2]

            self.q[2] = wrap_angle(self.q[2])

            # Étape 2 : Calcul des jacobiennes du modèle de processus
            # TODO: Définition de F et W
            F = np.array([])
            W = np.array([])

            # Étape 3: Faire l'estimation de covariance de l'état
            # TODO: à faire
            self.P = self.P

    def update(self, z: np.ndarray, tag_xy: np.ndarray):
        # z est la mesure sous la forme [range, bearing]
        # tag_xy est l'emplacement du AprilTag en coordonnées mondiales [tag_x, tag_y]

        with self.q_mutex:

            # Étape 1: calculer les mesures de portée et de relèvement prévues
            # TODO: mettre à jours les équations suivants
            rng_pred = 1.0
            bearing_pred = 0.0
            z_pred = np.array([rng_pred, bearing_pred])

            # Étape 2 : Calculer l'innovation
            # TODO: Trouver l'innovation y
            y = np.array([0.0, 0.0])
            y[1] = wrap_angle(y[1])

            # Étape 3 : Calculer le jacobien du modèle de mesure
            # TODO: Trouver H
            H = np.array([])

            # Étape 4 : Calculer le gain de Kalman
            # TODO: Trouver K
            K = np.array([])

            # Étape 5 : Mise à jour des estimations de pose et de covariance de pose
            # TODO: modifier les équations
            self.q = self.q
            self.q[2] = wrap_angle(self.q[2])
            self.P = self.P






