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
            theta = self.q[2] # angle actuel
            self.q[0] = self.q[0] + dX * np.cos(theta) # x
            self.q[1] = self.q[1] + dX * np.sin(theta) # y
            self.q[2] = self.q[2] + dT # theta (w)

            self.q[2] = wrap_angle(self.q[2])

            # Étape 2 : Calcul des jacobiennes du modèle de processus
            # TODO: Définition de F et W
            F = np.array([
                [1, 0, -dX * np.sin(theta)],
                [0, 1, dX * np.cos(theta)],
                [0, 0, 1]
            ])
            W = np.array([
                [np.cos(theta), 0],
                [np.sin(theta), 0], 
                [1, 0]
            ])

            # Étape 3: Faire l'estimation de covariance de l'état
            # TODO: à faire 
            self.P = F @ self.P @ F.T + W @ self.Q @ W.T

    def update(self, z: np.ndarray, tag_xy: np.ndarray):
        # z est la mesure sous la forme [range, bearing]
        # tag_xy est l'emplacement du AprilTag en coordonnées mondiales [tag_x, tag_y]

        with self.q_mutex:

            # Étape 1: calculer les mesures de portée et de relèvement prévues
            # TODO: mettre à jours les équations suivants
            dx = tag_xy[0] - self.q[0]
            dy = tag_xy[1] - self.q[1]
            # h
            rng_pred = np.sqrt(dx**2 + dy**2)
            bearing_pred = wrap_angle(np.arctan2(dy, dx) - self.q[2])
            z_pred = np.array([rng_pred, bearing_pred])

            # Étape 2 : Calculer l'innovation
            # TODO: Trouver l'innovation y
            y = z - z_pred
            y[1] = wrap_angle(y[1])

            # Étape 3 : Calculer le jacobien du modèle de mesure
            # TODO: Trouver H
            H = np.array([
                [-dx/rng_pred, -dy/rng_pred, 0],
                [dy/rng_pred**2, -dx/rng_pred**2, -1]
            ])

            # Étape 4 : Calculer le gain de Kalman
            # TODO: Trouver K
            # R = V @ R @ V.T
            K = self.P @ H.T @ np.linalg.inv(H @ self.P @ H.T + self.R)

            # Étape 5 : Mise à jour des estimations de pose et de covariance de pose
            # TODO: modifier les équations
            self.q = self.q + K @ y
            self.q[2] = wrap_angle(self.q[2])
            # P = (I - K*H) * P
            I = np.eye(self.P.shape[0])
            self.P = (I - K @ H) @ self.P


